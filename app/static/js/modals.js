$('#editTask').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var id = button.data('taskid')
    var modal = $(this)
    var content = $("#task"+id).html()
    modal.find('#editTaskForm textarea').html(content)
    modal.find('#editTaskForm').attr('action', 'update/' + id);
})
