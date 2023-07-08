/* libfuzzer test code for oniguruma
 * author: Hanno Böck, license: CC0/public domain

Usage:
* compile oniguruma with something like
	./configure CC=clang LD=clang CFLAGS="-fsanitize-coverage=edge -fsanitize=address" \
		LDFLAGS="-fsanitize-coverage=edge -fsanitize=address"
* Compile libfuzzer stub and link against static libonig.a and libFuzzer.a:
	clang++ libfuzzer-onig.cpp src/.libs/libonig.a libFuzzer.a -o libfuzzer-onig \
		-fsanitize-coverage=edge -fsanitize=address
* Put sample patterns in directory "in/"
* Run
	./libfuzzer-onig in

Consult libfuzzer docs for further details and how to create libFuzzer.a:
http://llvm.org/docs/LibFuzzer.html

 */
#include <stdint.h>
#include <string.h>
#include <oniguruma.h>

extern "C" int LLVMFuzzerTestOneInput(const uint8_t * Data, size_t Size)
{
	regex_t *reg;
	if (onig_new
	    (&reg, Data, Data + Size, ONIG_OPTION_DEFAULT, ONIG_ENCODING_UTF8,
	     ONIG_SYNTAX_DEFAULT, 0) == 0)
		onig_free(reg);
	return 0;
}
