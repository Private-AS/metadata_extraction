Get-EventLog -List
$eventLogs = Get-EventLog -List
$eventLogs | ConvertTo-Html -Property Log, MaximumKilobytes, RetentionDays, Entries -Title $env:COMPUTERNAME -PreContent "<h1>$env:COMPUTERNAME</h1><h2>Event logs</h2>"    | Out-File -FilePath ".\EventLogs.html"