
$settings = Get-Content -Raw -Encoding UTF8 settings.json | ConvertFrom-Json

$sourcePath = Resolve-Path $settings.path_jsonfiles
$themePath = Resolve-Path $settings.path_icontheme
$inkscape = Resolve-Path $settings.inkscape
$magick = Resolve-Path $settings.magick

foreach ($file in Get-ChildItem $sourcePath*json) 
{
    $json = Get-Content -Raw -Encoding UTF8 $file | ConvertFrom-Json

    foreach ($j in $json)
    {
        $output_path = Join-Path -Path $pwd.path -ChildPath "output" | Join-Path -ChildPath $j.path_out_ico
        New-Item -ItemType directory -Force -Path $output_path | Out-Null
        Write-Host("Process definition file: "+ $file)
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
                if($f.overlay)
                {
                    $inout = $(Join-Path -Path $output_path -ChildPath $output_file)
                    $input = Join-Path -Path $themePath -ChildPath $f.overlay.src
                    $output = '--export-filename="'+$(Join-Path -Path $output_path -ChildPath 'overlay.png')+'"'
                    $w='--export-width='+$f.overlay.size
                    $h='--export-height='+$f.overlay.size
                    & $inkscape $output $w $h $input | Wait-Process
                    & $magick convert $inout $(Join-Path -Path $output_path -ChildPath 'overlay.png') -gravity $f.overlay.gravity -composite $inout | Wait-Process
                    Remove-Item $(Join-Path -Path $output_path -ChildPath 'overlay.png')
                }
                if($f.canvas)
                {
                    $inout = $(Join-Path -Path $output_path -ChildPath $output_file)
                    & $magick convert $inout -gravity $f.canvas.gravity -background transparent -extent $([string]$f.canvas.size+"x"+[string]$f.canvas.size) $inout | Wait-Process
                }
            }
            $inp = Get-ChildItem $output_path -filter *.png | % { $_.FullName }
            $out = Join-Path -Path $output_path -ChildPath $i.file_out
            Write-Host("$([char]9)Convert to icon file: " + $i.file_out)
            & $magick convert $inp $out | Wait-Process
            Remove-Item $inp
        }
        $output_path = Join-Path -Path $pwd.path -ChildPath "output" | Join-Path -ChildPath $j.path_out_bmp
        New-Item -ItemType directory -Force -Path $output_path | Out-Null
        foreach ($i in $j.bitmap)
        {
            foreach ($f in $i.file_in)
            {
                $output_file = $i.file_out+'-'+$i.file_in.IndexOf($f) +'.png'
                $input = Join-Path -Path $themePath -ChildPath $f.src
                $output = '--export-filename="'+$(Join-Path -Path $output_path -ChildPath $output_file)+'"'
                $w='--export-width='+$i.size
                $h='--export-height='+$i.size
                & $inkscape $output $w $h $input | Wait-Process
            }
            $inp = Get-ChildItem $output_path -filter *.png | % { $_.FullName }
            $param = "+append"
            $out = Join-Path -Path $output_path -ChildPath $i.file_out
            Write-Host("$([char]9)Convert to bitmap file: " + $i.file_out)
            & $magick convert $inp $param $out | Wait-Process
            Remove-Item $inp
            $inp = $out
            $param = "-modulate"
            $param_val = "100,130"
            $out = Join-Path -Path $output_path -ChildPath $i.file_hov_out
            Write-Host("$([char]9)Convert to bitmap file: " + $i.file_hov_out)
            & $magick convert $inp $param $param_val $out | Wait-Process
        }
    }
}

