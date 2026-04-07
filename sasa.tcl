# isolated SASA per frame (no -restrict)
# outputs: frame  SASA_protein_iso  SASA_PROA_iso  SASA_PROB_iso

set n [molinfo top get numframes]

# --- output path
set output_dir "/path/to/output/file"
file mkdir $output_dir
set outfn [file join $output_dir "sasa_isolated.dat"]

set output [open $outfn w]
puts $output "frame sasa_protein_iso sasa_PROA_iso sasa_PROB_iso"

# selections
set sel_prot [atomselect top "protein"]
set sel_PROA [atomselect top "segname PROA and protein"]
set sel_PROB [atomselect top "segname PROB and protein"]

for {set i 0} {$i < $n} {incr i} {
    molinfo top set frame $i
    $sel_prot frame $i; $sel_prot update
    $sel_PROA frame $i; $sel_PROA update
    $sel_PROB frame $i; $sel_PROB update

    # Isolated SASA with 1.4 Å probe
    set sasa_prot [measure sasa 1.4 $sel_prot]
    set sasa_PROA [expr {([$sel_PROA num] > 0) ? [measure sasa 1.4 $sel_PROA] : double("nan")}]
    set sasa_PROB [expr {([$sel_PROB num] > 0) ? [measure sasa 1.4 $sel_PROB] : double("nan")}]

    puts $output "$i $sasa_prot $sasa_PROA $sasa_PROB"
}
close $output
puts "Wrote $outfn"
