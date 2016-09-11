$(function() {
    // setup search suggestions
    // @see https://goodies.pixabay.com/jquery/auto-complete/demo.html
    var field = $('#search input'),
        url = _g.suggest_url;

    field.autoComplete({
        source: function(term, response){
            $.getJSON(url, { q: term.toLowerCase() }, function(data) {
                response(data[1].slice(0, 10));
            });
        },
        onSelect: function() {
            $('#search form').submit();
        }
    });

    // auto-select cite box
    $('input.cite').on('click', function(ev) {
        $(this).select()
    });
});