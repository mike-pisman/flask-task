$(document).on('click', '.button-complete', function(){
    var taskId = $(this).data('task-id');
    let button = $(this);

    $.ajax({
        url: '/complete/' + taskId,
        type: 'POST',
        success: function (data) {
            // $(this).prop("checked", true);
            if (button.hasClass('done')) {
                button.removeClass('done').addClass('todo');
                addAlert('The task has been marked as todo', "info");
            } else {
                button.removeClass('todo').addClass('done');
                addAlert('The task has been marked as done', "success");
            }
            
        }
    });
  });