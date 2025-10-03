#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <tiffio.h>

void register_custom_tags(TIFF* tif, const TIFFFieldInfo* tags, int n) {
    TIFFMergeFieldInfo(tif, tags, n);
}

int write_custom_tag(const char* filename, ushort tag_code, const char* tag_name, const char* tag_value) {
    static const TIFFFieldInfo myCustomTags[] = {
        { 0, -1, -1, TIFF_ASCII, FIELD_CUSTOM, 1, 0, NULL } // placeholder
    };
    TIFFFieldInfo myTag = { tag_code, -1, -1, TIFF_ASCII, FIELD_CUSTOM, 1, 0, (char*)tag_name };
    TIFF* tif = TIFFOpen(filename, "r+");
    if (!tif) {
        fprintf(stderr, "Errore nell'apertura del file TIFF\n");
        return 1;
    }

    register_custom_tags(tif, &myTag, 1);
    if (TIFFSetField(tif, tag_code, tag_value) != 1) {
        fprintf(stderr, "Errore nell'impostare il tag custom\n");
        TIFFClose(tif);
        return 2;
    }

    if (!TIFFRewriteDirectory(tif)) {
        fprintf(stderr, "Errore nella riscrittura della directory\n");
        TIFFClose(tif);
        return 3;
    }

    TIFFClose(tif);
    printf("Tag custom scritto in %s con valore %s \n", filename, tag_value);
    return 0;
}
