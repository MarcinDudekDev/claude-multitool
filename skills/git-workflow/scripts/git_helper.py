#!/usr/bin/env python3
"""
Efficient Git workflow utilities - minimal output, maximum clarity
"""

import subprocess
import sys
from pathlib import Path

class GitHelper:
	def __init__(self):
		self.repo_root = self._get_repo_root()

	def _get_repo_root(self):
		"""Get git repository root"""
		try:
			result = subprocess.run(
				['git', 'rev-parse', '--show-toplevel'],
				capture_output=True,
				text=True,
				check=True
			)
			return result.stdout.strip()
		except subprocess.CalledProcessError:
			sys.exit("Error: Not in a git repository")

	def quick_status(self):
		"""Show quick summary of changes"""
		try:
			# Modified files
			modified = subprocess.run(
				['git', 'diff', '--name-only'],
				capture_output=True,
				text=True,
				check=True
			).stdout.strip().split('\n')

			# Staged files
			staged = subprocess.run(
				['git', 'diff', '--cached', '--name-only'],
				capture_output=True,
				text=True,
				check=True
			).stdout.strip().split('\n')

			# Untracked files
			untracked = subprocess.run(
				['git', 'ls-files', '--others', '--exclude-standard'],
				capture_output=True,
				text=True,
				check=True
			).stdout.strip().split('\n')

			modified = [f for f in modified if f]
			staged = [f for f in staged if f]
			untracked = [f for f in untracked if f]

			print(f"Modified: {len(modified)} | Staged: {len(staged)} | Untracked: {len(untracked)}")
			
			if modified:
				print(f"\nModified: {', '.join(modified)}")
			if staged:
				print(f"Staged: {', '.join(staged)}")
			if untracked:
				print(f"Untracked: {', '.join(untracked)}")

		except subprocess.CalledProcessError as e:
			sys.exit(f"Git error: {e}")

	def add_all(self):
		"""Stage all changes"""
		try:
			subprocess.run(['git', 'add', '.'], check=True)
			print("✓ All changes staged")
			self.quick_status()
		except subprocess.CalledProcessError as e:
			sys.exit(f"Error staging files: {e}")

	def last_commit_info(self):
		"""Show last commit with author info"""
		try:
			result = subprocess.run(
				['git', 'log', '-1', '--pretty=format:%h | %an | %s'],
				capture_output=True,
				text=True,
				check=True
			)
			print(f"Last commit: {result.stdout}")
		except subprocess.CalledProcessError:
			print("No commits yet")

	def show_diff(self, staged=False):
		"""Show diff of changes"""
		try:
			cmd = ['git', 'diff']
			if staged:
				cmd.append('--cached')
			subprocess.run(cmd, check=True)
		except subprocess.CalledProcessError as e:
			sys.exit(f"Error showing diff: {e}")

	def branch_info(self):
		"""Show current branch and tracking"""
		try:
			branch = subprocess.run(
				['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
				capture_output=True,
				text=True,
				check=True
			).stdout.strip()

			tracking = subprocess.run(
				['git', 'rev-parse', '--abbrev-ref', '@{u}'],
				capture_output=True,
				text=True
			).stdout.strip()

			print(f"Branch: {branch}", end="")
			if tracking and tracking != '@{u}':
				print(f" → {tracking}")
			else:
				print(" (no upstream)")
		except subprocess.CalledProcessError as e:
			sys.exit(f"Error getting branch info: {e}")

def main():
	if len(sys.argv) < 2:
		print("Usage: git_helper.py <command>")
		print("Commands:")
		print("  status       - Quick change summary")
		print("  add-all      - Stage all changes")
		print("  last         - Show last commit")
		print("  diff         - Show unstaged changes")
		print("  diff-staged  - Show staged changes")
		print("  branch       - Show current branch info")
		sys.exit(1)

	helper = GitHelper()
	command = sys.argv[1]

	if command == 'status':
		helper.quick_status()
	elif command == 'add-all':
		helper.add_all()
	elif command == 'last':
		helper.last_commit_info()
	elif command == 'diff':
		helper.show_diff(staged=False)
	elif command == 'diff-staged':
		helper.show_diff(staged=True)
	elif command == 'branch':
		helper.branch_info()
	else:
		sys.exit(f"Unknown command: {command}")

if __name__ == '__main__':
	main()
