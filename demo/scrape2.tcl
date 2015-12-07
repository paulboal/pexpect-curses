#!/usr/bin/expect

set timeout 2
#log_user 0
spawn -noecho "./demo2.py"

set accum {}

proc term_wait { } {
	set a {}
	expect {
		-regexp { ..* } {
			set a "${a}$expect_out(0,string)"
			exp_continue
		}
	}
	return ${a}
}

set b [term_wait]
set accum "${accum}${b}"
puts [format "%d" [string length $accum]]

send "A"

set b [term_wait]
set accum "${accum}${b}"

puts "Timed out"
puts [format "%d" [string length $accum]]
