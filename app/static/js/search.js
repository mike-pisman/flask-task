$(function(){
    $("#listSearchInput").on("keyup", function() {
        var value = $(this).val().toLowerCase();

        $("table tr").each(function(index) {
            if (index != 0) {

                $row = $(this);

                var name = $row.find(".list-name").text();

                if (name.toLowerCase().indexOf(value) == -1) {
                    $(this).hide();
                }
                else {
                    $(this).show();
                }
            }
        });
    });
});