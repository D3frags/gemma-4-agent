from functions.get_files_info import get_files_info

print("Results for current directory:")
print(get_files_info("calculator", "."))
print()
print("Results for 'pkg' directory:")
print(get_files_info("calculator", "pkg"))
print()
print("Results for '/bin' directory:")
print(get_files_info("calculator", "/bin"))
print()
print("Results for '../' directory:")
print(get_files_info("calculator", "../"))
