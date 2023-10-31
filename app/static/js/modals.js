$('#editTask').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var id = button.parent().parent().parent().data('task-id')

    var modal = $(this)
    var content = $("#task_"+id).find('.task-content').html()
    modal.find('#editTaskForm textarea').html(content)
    modal.find('#editTaskForm').attr('action', 'update/' + id);
})
