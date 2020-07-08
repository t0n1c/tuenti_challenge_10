#!/usr/bin/env bash
    
    
    chr() {
        printf \\$(printf '%03o' $1)
    }
    
    function hex() {
        printf '%02X\n' $1
    }
    
    function encrypt() {
        key=$1
        msg=$2
        crpt_msg=""
        for ((i=0; i<${#msg}; i++)); do
            c=${msg:$i:1}
            asc_chr=$(echo -ne "$c" | od -An -tuC)
            key_pos=$((${#key} - 1 - ${i}))
            key_char=${key:$key_pos:1}
            crpt_chr=$(( $asc_chr ^ ${key_char} )) #exclusive XOR
            hx_crpt_chr=$(hex $crpt_chr) # hex repre
            crpt_msg=${crpt_msg}${hx_crpt_chr} # concat
        done
        echo $crpt_msg
    }

    function test_encrypt() {
        key=$1
        msg=$2
        crpt_msg=""
        for ((i=0; i<${#msg}; i++)); do
             c=${msg:$i:1}
             asc_chr=$(echo -ne "$c" | od -An -tuC) # digit to asc
             #echo $asc_chr
             key_pos=$((${#key} - 1 - ${i}))
             #echo $key_pos
             key_char=${key:$key_pos:1}
             #echo $key_char
             crpt_chr=$(( $asc_chr ^ ${key_char} )) #exclusive XOR
             #echo $crpt_chr
             hx_crpt_chr=$(hex $crpt_chr) # hex repre
             crpt_msg=${crpt_msg}${hx_crpt_chr} # concat
        done
        echo $crpt_msg
    }

# encrypt $1 $2
#key=$1
#echo ${#key} len
test_encrypt $1 $2

# message: 514;248;980;347;145;332
# key???
# encrypeted: 3633363A33353B393038383C363236333635313A353336
#
# xxx;yyy;zzz;aaa;bbb;ccc (coordinates have 6 componenents 
# exactly 23 characters) always
# 
# 3633363A33353B393038383C363236333635313A353336
# 3A3A333A333137393D39313C3C3634333431353A37363D

