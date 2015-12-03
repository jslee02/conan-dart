function main($cloned_repo_dir)
{
  # Add CONAN path to the Path environment variables
  $cloned_repo_dir = 'C:\projects\conan-dart'
  $command = 'setx Path "' + $cloned_repo_dir + ';' + [System.Environment]::GetEnvironmentVariable("Path", "User") + '"'
  iex $command

  # Reload Path
  $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

}

main
