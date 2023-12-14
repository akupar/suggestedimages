(function () {
    const kielikoodit = {
        'Englanti': 'en',
        'Espanja': 'es',
        'Ruotsi': 'sv',
        'Saksa': 'de',
        'Suomi': 'fi',
    };

    $('h2').each(function () {
        const kieli = $(this).children('.mw-headline').text();
	console.log("kieli", kieli, kielikoodit[kieli]);
        if ( kielikoodit[kieli] ) {
            const sivu = mw.config.get('wgTitle');
            const url = 'http://127.0.0.1:5000/?' + $.param({
                wikt: 'fi',
                lang: kielikoodit[kieli],
                title: encodeURIComponent(sivu),
            });
	    $(this).append(' ', $('<a target="_BLANK" title="Etsi kuvia">🖼</a>').attr('href', url));
        }
    });
}());
