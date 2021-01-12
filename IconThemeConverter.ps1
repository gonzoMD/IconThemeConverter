
$settings = Get-Content -Raw -Encoding UTF8 settings.json | ConvertFrom-Json

$sourcePath = Resolve-Path $settings.path_jsonfiles
$themePath = Resolve-Path $settings.path_icontheme
$inkscape = Resolve-Path $settings.inkscape
$convert = Resolve-Path $settings.convert

foreach ($file in Get-ChildItem $sourcePath*json) 
{
    $json = Get-Content -Raw -Encoding UTF8 $file | ConvertFrom-Json

    foreach ($j in $json)
    {
        $output_path = Join-Path -Path $pwd.path -ChildPath "output" | Join-Path -ChildPath $j.path_out
        New-Item -ItemType directory -Force -Path $output_path
        
        foreach ($i in $j.icon)
        {
            foreach ($f in $i.file_in)
            {
                $output_file = $i.file_out+'-'+$f.size +'.png'
                $input = Join-Path -Path $themePath -ChildPath $f.src
                $output = '--export-filename="'+$(Join-Path -Path $output_path -ChildPath $output_file)+'"'
                $w='--export-width='+$f.size
                $h='--export-height='+$f.size
                & $inkscape $output $w $h $input | Wait-Process
            }
            $inp = Get-ChildItem $output_path -filter *.png | % { $_.FullName }
            $out = Join-Path -Path $output_path -ChildPath $i.file_out
            & $convert $inp $out | Wait-Process
            Remove-Item $inp
        }
    }
}

