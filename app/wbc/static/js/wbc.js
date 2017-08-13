$(function() {
    // setup search suggestions
    // @see https://goodies.pixabay.com/jquery/auto-complete/demo.html
    var field = $('#search input'),
        url = _g.suggest_url,
        xhr;

    function highlight(item, query) {
        query = query.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
        var re = new RegExp("(" + query.split(' ').join('|') + ")", "gi");

        return item.replace(re, "<b>$1</b>");
    }

    field.autoComplete({
        source: function(term, response){
            try { xhr.abort(); } catch(e){}
            xhr = $.getJSON(url, { q: term.toLowerCase() }, function(data) {
                var suggestions = [];

                // keyword suggestions
                data[1].slice(0, 10).forEach(function(item) {
                    suggestions.push(item);
                });

                // publications suggest
                data[2].forEach(function(item) {
                    suggestions.push('<div class="autocomplete-suggestion" data-url="' + item.url + '">' +
                        highlight(item.name, data[0]) +
                        '<small>' + item.info + '</small></div>');
                });

                console.log(suggestions);
                response(suggestions);
            });
        },
        renderItem: function (item, search){
            // item is already rendered by source()
            if (item[0] === '<') {
                return item;
            }

            // plain text suggestion
            return '<div class="autocomplete-suggestion" data-val="' + item + '">' + highlight(item, search) + '</div>';
        },
        onSelect: function(event, term, item) {
            var url = item.data('url');
            if (url) {
                document.location = url;
                event.preventDefault();
            }
            else {
                $('#search form').submit();
            }
        }
    });

    // auto-select cite box
    $('input.cite').on('click', function(ev) {
        $(this).select()
    });
});