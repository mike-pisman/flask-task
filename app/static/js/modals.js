$('#editTask').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var id = button.parent().parent().parent().data('task-id')

    var modal = $(this)
    var content = $("#task_"+id).find('.task-content').html()
    $('#editTaskForm').find('textarea').html(content)
    $('#editTaskForm').attr('action', 'tasks/' + id);
    $('#editTaskForm').attr('data-task-id', id);
})
