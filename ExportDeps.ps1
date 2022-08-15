foreach ($projects in (Get-ChildItem . -Directory)) {
	& python -m venv $projects
	foreach ($dir in (Get-ChildItem $projects -Directory)) {
		if($dir.BaseName -eq "Scripts") {
			$name = $dir.FullName
			& "$name\\Activate.ps1" & pip freeze & "$name\\deactivate.bat"
			break;
		}
	}
}