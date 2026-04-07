# set paths for output files
set output_path_A "/path/to/output/file/"
set output_path_B "/path/to/output/file/"

set output_A [open $output_path_A w]
set output_B [open $output_path_B w]

puts $output_A "idx resid rmsf_all"
puts $output_B "idx resid rmsf_all"

# define number of frames 
set n [molinfo top get numframes]
set ls [expr {$n - 1}]

# select all atoms so the entire system moves during alignment
set sel_all [atomselect top "all"]

# ==========================================
# phase 1: align on PROA & calculate PROA
# ==========================================
set ref_A [atomselect top "segname PROA and name CA" frame 0]
set comp_A [atomselect top "segname PROA and name CA"]

# fit the frames to PROA
for {set i 0} {$i < $n} {incr i} {
    $comp_A frame $i
    $sel_all frame $i
    set trans_mat [measure fit $comp_A $ref_A]
    # Move all atoms to preserve the integrity of the molecule
    $sel_all move $trans_mat
}

# calculate RMSF for PROA
set rmsfa_A [measure rmsf $comp_A first 0 last $ls step 1]

# write PROA results to file
set res_A [$comp_A get resid]
for {set i 0} {$i < [$comp_A num]} {incr i} {
    puts $output_A "[expr {$i+1}] [lindex $res_A $i] [lindex $rmsfa_A $i]"
}

# ==========================================
# phase 2: align on PROB & calculate PROB
# ==========================================
set ref_B [atomselect top "segname PROB and name CA" frame 0]
set comp_B [atomselect top "segname PROB and name CA"]

# fit the frames to PROB
for {set i 0} {$i < $n} {incr i} {
    $comp_B frame $i
    $sel_all frame $i
    set trans_mat [measure fit $comp_B $ref_B]
    # Move all atoms based on PROB alignment
    $sel_all move $trans_mat
}

# calculate RMSF for PROB 
set rmsfa_B [measure rmsf $comp_B first 0 last $ls step 1]

# write PROB results to file
set res_B [$comp_B get resid]
for {set i 0} {$i < [$comp_B num]} {incr i} {
    puts $output_B "[expr {$i+1}] [lindex $res_B $i] [lindex $rmsfa_B $i]"
}

# clean up
close $output_A
close $output_B

$ref_A delete
$comp_A delete
$ref_B delete
$comp_B delete
$sel_all delete

puts "RMSF calculation complete. Saved to $output_path_A and $output_path_B"

# Delete all molecules (optional)
# mol delete all