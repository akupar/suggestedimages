(function () {
    const WIKTIONARY = 'fi';
    const language_heading_to_code = {
        'Englanti': 'en',
        'Espanja': 'es',
        'Ruotsi': 'sv',
        'Saksa': 'de',
        'Suomi': 'fi',
    };

    $('h2').each(function () {
        const language = $(this).children('.mw-headline').text();
        if ( language_heading_to_code[language] ) {
            const title = mw.config.get('wgTitle');
            const url = 'https://imgs-for-wikt.toolforge.org/?' + $.param({
                wikt: WIKTIONARY,
                lang: language_heading_to_code[language],
                title: title,
            });
	    $(this).append(' ', $('<a target="_BLANK" title="Image search">🖼</a>').attr('href', url));
        }
    });
}());
