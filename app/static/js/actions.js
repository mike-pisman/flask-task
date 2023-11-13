// Check if task list is empty on page load
$(document).ready(function(){
    hideTableIfEmpty();

    $('#createListForm').submit(function(e){
        e.preventDefault();
        list = $(this).serialize();
        createList(list);
        return false;
    });
});

// Open list page on row click
$(document).on('click', '.list-name', function(){
    console.log('clicked');
    window.open("/lists/" + $(this).parent().data('list-id') + "/tasks", "_self");
});

// Hide task list if empty
hideTableIfEmpty = function() {
    let message = $('#emptyListMessage');
    let table = $('#table');
    let tableLength = $('#table tr').length;
    if (tableLength == 1) {
        table.css('display', 'none');
        message.css('display', 'block');
    } else {
        table.css('display', 'table');
        message.css('display', 'none');
    }
}

// Get list ID from URL
getListID = function() {
    let current_page = window.location.href;
    let listID = current_page.match(/\/lists\/(\d+)\/tasks/)[1];
    if (listID == null) {
        return false;
    }
    return listID;
}

// Process complete-task button
$(document).on('click', '.complete-task', function(){
    let taskId = $(this).parent().parent().parent().data('task-id');
    let button = $(this);

    completeTask(taskId, button)
});

// Process delete-task button
$(document).on('click', '.delete-task', function(){
    let taskId = $(this).parent().parent().parent().data('task-id');

    deleteTask(taskId);
});

// Mark task as done or todo
completeTask = function(taskID, button) {
    let listID = getListID();

    $.ajax({
        url: `/api/lists/${listID}/tasks/${taskID}`,
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

// Delete task
deleteTask = function() {
    let taskID = $('#deleteTaskModal').data('task-id')
    let listID = getListID();
    $.ajax({
        url: `/api/lists/${listID}/tasks/${taskID}`,
        type: 'DELETE',
        success: function () {
            $('#deleteTaskModal').modal('hide');
            $('#task_'+taskID).remove();
            addAlert('The task has been deleted', "success");
            hideTableIfEmpty();
        },
        error: function () {
            addAlert('The task could not be deleted', "danger");
        }
    });
}

// Create task
createTask = function() {
    let formData = $('#createTaskForm').serialize();
    let listID = getListID();

    $.ajax({
        url: `/api/lists/${listID}/tasks`,
        type: 'POST',
        data: formData,
        success: function (response) {
            newTask = JSON.parse(response).task;
            $('#createTaskModal').modal('hide');
            $('#createTaskForm').trigger('reset');
            addAlert('The task has been created', "success");

            newRow = $('<tr id="task_' + newTask.id + '" data-task-id="' + newTask.id + '"></tr>');
            completed = $(`
                <td class="task-check">
                    <todo-task-button></todo-task-button>
                </td>
            `);
            date = $('<td class="task-date">' + (new Date(newTask.date_created + 'Z')).toLocaleString().replace(/,/g, '') + '</td>');
            content = $('<td class="task-content"></td>').text(newTask.content);
            actions = $(`
                <td class="task-actions">
                    <edit-button target="#editTaskModal"></edit-button>
                    <delete-button target="#deleteTaskModal"></delete-button>
                </td>
            `);

            newRow.append(completed, date, content, actions);
            $('#table').append(newRow);
            hideTableIfEmpty();
        },
        error: function () {
            addAlert('The task could not be created', "danger");
        }
    });
}

// Update task
updateTask = function() {
    taskContent = $('#editTaskForm').find('textarea').val();
    formData = $('#editTaskForm').serialize();
    taskID = $('#editTaskForm').data('task-id')
    listID = getListID();

    $.ajax({
        url: `/api/lists/${listID}/tasks/${taskID}`,
        type: 'PATCH',
        data: formData,
        success: function () {
            $('#editTaskModal').modal('hide');
            $('#editTaskForm').trigger('reset');
            addAlert('The task has been updated', "success");
            $('#task_' + taskID).find('.task-content').text(taskContent);
        },
        error: function () {
            addAlert('The task could not be created', "danger");
        }
    });
}

// Create task list
createList = function(list) {
    $.ajax({
        url: '/api/lists',
        type: 'POST',
        data: list,
        success: function (response) {
            let newList = JSON.parse(response).list;
            addAlert('The task list has been created', "success");
            $('#createListModal').modal('hide');
            $('#createListForm').trigger('reset');

            let newRow = $('<tr id="list_' + newList.id + '" data-list-id="' + newList.id + '" class="list-row"></tr>');
            let name = $('<td class="list-name"></td>').text(newList.name);
            let actions = $(`
                <td class="task-actions">
                    <edit-button target="#editListModal"></edit-button>
                    <delete-button target="#deleteListModal"></delete-button>
                </td>
            `);

            newRow.append(name, actions);
            console.log(newRow);
            $('#table').append(newRow);
            hideTableIfEmpty();
        },
        error: function () {
            addAlert('The task list could not be created', "danger");
        }
    });
}

// Update task list
updateList = function() {
    listName = $('#editListForm').find('input').val();
    formData = $('#editListForm').serialize();
    listID = $('#editListForm').data('list-id')

    $.ajax({
        url: '/api/lists/' + listID,
        type: 'PATCH',
        data: formData,
        success: function () {
            $('#editListModal').modal('hide');
            $('#editListForm').trigger('reset');
            addAlert('The task list has been updated', "success");
            $('#list_' + listID).find('.list-name').text(listName);
        },
        error: function () {
            addAlert('The task list could not be updated', "danger");
        }
    });
}

// Delete task list
deleteList = function() {
    let listID = $('#deleteListModal').data('list-id')
    $.ajax({
        url: '/api/lists/' + listID,
        type: 'DELETE',
        success: function () {
            $('#deleteListModal').modal('hide');
            addAlert('The task list has been deleted', "success");
            $('#list_' + listID).remove();
            hideTableIfEmpty();
        },
        error: function () {
            addAlert('The task list could not be deleted', "danger");
        }
    });
}