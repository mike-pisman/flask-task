$(document).ready(function(){
    hideListIfEmpty();
});

hideListIfEmpty = function() {
    let message = $('#emptyListMessage');
    let list = $('#taskList');
    let listLength = $('#taskList tr').length;
    if (listLength == 1) {
        list.css('display', 'none');
        message.css('display', 'block');
    } else {
        list.css('display', 'table');
        message.css('display', 'none');
    }
}

$(document).on('click', '.complete-task', function(){
    let taskId = $(this).parent().parent().parent().data('task-id');
    let button = $(this);

    completeTask(taskId, button)
});

$(document).on('click', '.delete-task', function(){
    let taskId = $(this).parent().parent().parent().data('task-id');

    deleteTask(taskId);
});


completeTask = function(taskId, button) {
    $.ajax({
        url: '/tasks/' + taskId,
        type: 'POST',
        success: function () { 
            if (button.hasClass('done')) {
                button.removeClass('done').addClass('todo');
                addAlert('The task has been marked as todo', "info");
            } else {
                button.removeClass('todo').addClass('done');
                addAlert('The task has been marked as done', "success");
            }
            
        }
    });
}


deleteTask = function(taskId) {
    $.ajax({
        url: '/tasks/' + taskId,
        type: 'DELETE',
        success: function () {
            $('#task_'+taskId).remove();
            addAlert('The task has been deleted', "success");
            hideListIfEmpty();
        }
    });
}


createTask = function() {
    formData = $('#createTaskForm').serialize();

    $.ajax({
        url: '/tasks',
        type: 'POST',
        data: formData,
        success: function (response) {
            newTask = JSON.parse(response).task;
            $('#createTask').modal('hide');
            $('#createTaskForm').trigger('reset');
            addAlert('The task has been create', "success");

            newRow = $('<tr id="task_' + newTask.id + '" data-task-id="' + newTask.id + '"></tr>');
            completed = $(`
                <td class="task-check">
                    <todo-task-button></todo-task-button>
                </td>
            `);
            date = $('<td class="task-date">' + newTask.date_created + '</td>');
            content = $('<td class="task-content"></td>').text(newTask.content);
            actions = $(`
                <td class="task-actions">
                    <edit-task-button></edit-task-button>
                    <delete-task-button></delete-task-button>
                </td>
            `);

            newRow.append(completed, date, content, actions);
            $('#taskList').append(newRow);
            hideListIfEmpty();
        },
        error: function () {
            addAlert('The task could not be created', "danger");
        }
    });
}

updateTask = function() {
    taskContent = $('#editTaskForm').find('textarea').val();
    formData = $('#editTaskForm').serialize();
    taskID = $('#editTaskForm').data('task-id')

    $.ajax({
        url: '/tasks/' + taskID,
        type: 'PATCH',
        data: formData,
        success: function () {
            $('#editTask').modal('hide');
            $('#editTaskForm').trigger('reset');
            addAlert('The task has been updated', "success");
            $('#task_' + taskID).find('.task-content').text(taskContent);
        },
        error: function () {
            addAlert('The task could not be created', "danger");
        }
    });
}