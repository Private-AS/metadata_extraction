Get-Process | Where-Object { $_.StartTime -ne $null } | `
    Sort-Object StartTime | `
    Select-Object -First 25 Id, Name, StartTime, 
    @{Name='Duration'; Expression={ (Get-Date) - $_.StartTime}},
    Path | `
    Export-Csv -Path ".\Processes.csv" -NoTypeInformation -Encoding UTF8