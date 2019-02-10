#!/bin/bash

sbcl --disable-debugger --noprint --eval "(compile-file \"$1\")" --quit
