# Row sets and how to rebuild the windows

Raw windows are not redistributed. Every window's SHA-256 is in `manifest.json`; `beyond_compressor.py verify` checks a
rebuilt array against it. Windows are 4095 raw bytes; models are scored with the one-byte prefix `O` (0x4F), the
compressors on the raw window.

**26 benchmark labels (`bench__*`).** Six ship with the original release; the other 20 are rebuilt with the original
authors' released bake scripts, run unchanged (their benchmark data description gives the sources). The first 256
rows of each label are used (fewer where a corpus has fewer).

**8 earlier sources (`new__hewiki`, `new__dewiki`, `new__go_source`, `new__fashion_mnist`, `new__elf_x86_64`,
`new__uci_adult`, `new__yesno_pcm16`, `new__python_docs_html`).** Fixed before download (project Battery 87):
Hebrew and German Wikipedia (first parquet shard of `wikimedia/wikipedia`, configs `20231101.he` and `20231101.de`,
field `text`); every `.go` file under `src/` of go.dev/dl/go1.22.5.src.tar.gz; Fashion-MNIST
`train-images-idx3-ubyte.gz`, header removed; ELF files under /usr/bin and /usr/lib/x86_64-linux-gnu of the build
image (Modal debian_slim, Python 3.11; not exactly reproducible elsewhere, so verify by hash); UCI Adult
`adult.data`, one line per document; OpenSLR SLR1 yes/no recordings, 16-bit PCM, headers removed; the Python 3.12
HTML documentation archive. Documents are shuffled with `numpy.random.default_rng(870)`, concatenated to 8,388,608
bytes, and 256 windows start at offsets i * floor((len - 4095) / 255), i = 0..255. Builder: `rebuild/b87_modal.py`, an original-project recipe that runs in the cloud (Modal) and depends on
the project layout; the download hashes recorded at build time are in `rebuild/b87_build.json`.

**6 sources fixed before download (`new__gutenberg_en`, `new__rust_ripgrep`, `new__js_lodash`,
`new__json_countries`, `new__kmnist_images`, `new__fsdd_audio`; project Battery 106).** Project Gutenberg texts 2701,
1342 and 84 concatenated; all `*.rs` files of ripgrep 14.1.1 and all `*.js` files of lodash 4.17.21, sorted by path;
mledoze/countries `countries.json`; KMNIST training images (raw uint8, array order); Free Spoken Digit Dataset
v1.0.10, sorted by file name, PCM mapped to 8 bits as ((s >> 8) + 128) mod 256 for 16-bit input, headers removed. Each
stream is capped at 8 MB, cut into consecutive 4095-byte windows, and 256 windows are drawn without replacement with
numpy seed 1060. Builder: `rebuild/b106_modal.py` (same caveats); source pins recorded at download are in
`rebuild/b106_provenance.json`.
