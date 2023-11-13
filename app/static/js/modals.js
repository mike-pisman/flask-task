$('#editTaskModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var id = button.parent().parent().parent().data('task-id')
    var content = $("#task_"+id).find('.task-content').html()
    $('#editTaskForm').find('textarea').html(content)
    $('#editTaskForm').attr('action', 'tasks/' + id);
    $('#editTaskForm').attr('data-task-id', id);
})

$('#editListModal').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget) // Button that triggered the modal
    let id = button.parent().parent().parent().data('list-id')
    let name = $("#list_"+id).find('.list-name').html()
    $('#editListForm').find('input').val(name)
    $('#editListForm').attr('action', 'lists/' + id);
    $('#editListForm').attr('data-list-id', id);
})

$('#deleteTaskModal').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget) // Button that triggered the modal
    let id = button.parent().parent().parent().data('task-id')
    $('#deleteTaskModal').data('task-id', id);
})

$('#deleteListModal').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget) // Button that triggered the modal
    let id = button.parent().parent().parent().data('list-id')
    $('#deleteListModal').data('list-id', id);
})