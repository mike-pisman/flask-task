$(function(){
    $("#listSearchInput").on("keyup", function() {
        var value = $(this).val().toLowerCase().split(" ");

        $("table tr").each(function(index) {
            if (index != 0) {

                $row = $(this);

                var name = $row.find(".list-name").text();

                $(this).show();
                for (i in value) {
                    if (name.toLowerCase().indexOf(value[i]) == -1) {
                        $(this).hide();
                        break;
                    }
                }
            }
        });
    });
});

$(function(){
    $("#taskSearchInput").on("keyup", function() {
        var value = $(this).val().toLowerCase().split(" ");

        $("table tr").each(function(index) {
            if (index != 0) {

                $row = $(this);

                var name = $row.find(".task-content").text();

                $(this).show();
                for (i in value) {
                    if (name.toLowerCase().indexOf(value[i]) == -1) {
                        $(this).hide();
                        break;
                    }
                }
            }
        });
    });
});