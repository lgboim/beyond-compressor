# Compressor logging patches

Both files are full replacement source files, modified to log per-byte log losses; the lpaq1 file also keeps the
input-mask control (`LPAQ_MASK`) used in the paper's masking diagnostic.

**paq8px** (`paq8px_Encoder_logging.cpp` replaces `src/Encoder.cpp`):

    git clone https://github.com/hxim/paq8px.git && cd paq8px
    git checkout c84f576fc2c522194cd320743708652a154daf6b
    cp ../paq8px_Encoder_logging.cpp src/Encoder.cpp
    mkdir -p build && cd build && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j8
    PAQ_BITLOG=log.bin ./paq8px -8 window.bin      # standard mode; add -forcetext or -forcebinary for forced mode

With `PAQ_BITLOG` set, the encoder writes, for every coded byte, a main-predictor flag, the byte value and the sum of
-log2 p over its eight bit predictions. Archive sizes are unchanged by the patch. Licence: GNU General Public License, version 2 or later, as stated in the License section of the paq8px README at
this commit; text in `COPYING.GPL-2.0`.

**lpaq1** (`lpaq1_logging.cpp`, lpaq1 by Matt Mahoney, 2007):

    g++ -O2 lpaq1_logging.cpp -o lpaq1_logging
    LPAQ_MASK=127 LPAQ_LOG=log.bin ./lpaq1_logging 4 window.bin window.lpaq

`LPAQ_MASK=127` is the full model (all inputs; the released per-byte data use this setting and level 4).
Licence: GNU General Public License, version 2 or later (text in `COPYING.GPL-2.0`).

**Basic compressor of Section 3.6** (`lpaq1_frozen.cpp`: lpaq1 with switchable upgrades, frozen before Battery 117;
SHA-256 0b670427861aa6d562099f00e78f3d6d96f4d8dcb0026366cff94ca5347387f7):

    g++ -O2 lpaq1_frozen.cpp -o lpaq1_frozen
    LPAQ_MASK=127 LPAQ_UP=126975 LPAQ_LOG=log.bin ./lpaq1_frozen 4 window.bin window.lpaq   # the frozen variant
    LPAQ_UP=126975 ./lpaq1_frozen d window.lpaq window.out                                  # decompress (same LPAQ_UP)

`LPAQ_UP=0` gives the original lpaq1 (byte-identical output). The switches are listed at the top of the file.
Licence: as lpaq1, GNU General Public License, version 2 or later.
