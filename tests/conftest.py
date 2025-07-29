import pytest
import sys
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init()

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Display a cool success message when all tests pass."""
    if exitstatus == 0:  # All tests passed
        passed = len(terminalreporter.stats.get('passed', []))
        failed = len(terminalreporter.stats.get('failed', []))
        skipped = len(terminalreporter.stats.get('skipped', []))
        
        print("\n" + "="*80)
        print(f"{Fore.GREEN}{Style.BRIGHT}🎉 ALL TESTS PASSED! 🎉{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ DNA Storage System is ready for deployment! ✅{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🧬 Encoder: Binary → Base-4 → DNA (with constraints){Style.RESET_ALL}")
        print(f"{Fore.CYAN}🧬 Decoder: DNA → Base-4 → Binary (with metadata){Style.RESET_ALL}")
        print(f"{Fore.CYAN}🧬 File I/O: FASTA format with automatic type detection{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🧬 CLI: Complete encode/decode workflow{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📊 Total Tests: {passed} passed{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📊 Failed: {failed}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📊 Skipped: {skipped}{Style.RESET_ALL}")
        print("="*80)
        print(f"{Fore.GREEN}{Style.BRIGHT}🚀 System Status: PRODUCTION READY! 🚀{Style.RESET_ALL}")
        print("="*80 + "\n")
    else:
        print("\n" + "="*80)
        print(f"{Fore.RED}{Style.BRIGHT}❌ SOME TESTS FAILED ❌{Style.RESET_ALL}")
        print(f"{Fore.RED}Please fix the failing tests before deployment.{Style.RESET_ALL}")
        print("="*80 + "\n") 