
function checkStatuses() {
	$('.one-task .status').each(function (e, t) {
		var $th = $(this);
		var html = $th.html();
		switch (html) {
			case '0':
				$th.html('Created');
				$th.addClass('created');
				break;
			case '1':
				$th.html('Active');
				$th.addClass('active');
				break;
			case '2':
				$th.html('Completed');
				$th.addClass('completed');
		}
	});
}

function completeSub(subId) {
	$.ajax({
		url: '/completeSubTask',
		type: 'POST',
		data: {
			taskId: subId
		},
		success: function(response){
			console.log(response)
		},
		error: function (resp) {
			console.log(resp)
		}
	});
}

function removeTask(taskId) {
	$.ajax({
		url: '/removeTask',
		type: 'POST',
		data: {
			taskId: taskId
		},
		success: function(response){
			console.log(response);
			getTasks();
		},
		error: function (resp) {
			console.log(resp)
		}
	});
}

function removeSubTask(subId) {
	$.ajax({
		url: '/removeSubTask',
		type: 'POST',
		data: {
			taskId: subId
		},
		success: function(response){
			console.log(response);
			getTasks($('[data-subtaskid='+subId+']').parents('.one-task').attr('data-taskId'));
		},
		error: function (resp) {
			console.log(resp)
		}
	});
}

function checkSubList($th) {
	var compl = $th.parents('.sublist-block').find('.one-subtask:not(".completed")').length;
	if (compl>0){
		return
	}
	var task = $th.parents('.one-task');
	setTask(task, 2);
}

function setTask(task, status) {
	task.find('.first_lane.status').html(status);
	checkStatuses();
}

function thisTask($th){
	$('.full-view').off('mousedown');
	if (!$th.hasClass('full-view')) {
		closeTasks();
		$th.addClass('full-view')
	}
	$('.full-view').off('mousedown');
	$('.one-task.full-view').mousedown(function (e) {
		var tg = $(e.target);
		if (tg.hasClass('first_lane')){
			setTimeout(function () {
				$('.full-view').off('mousedown');
				closeTasks();
			},200);
		}
	})
}

function closeTasks(){
	$('.full-view').removeClass('full-view');
}

function closeModals(){
	$('form').find('.form-control').val('');
	$('.showed').removeClass('showed');
}

function getTasks(setId){
	$.ajax({
		url: '/getTasks',
		type: 'GET',
		success: function(response){
			console.log(response);
			$('#tasks').html(response);
			functionality();
			closeTasks();
			closeModals();
			if (setId!=undefined){
				thisTask($('[data-taskId='+setId+']').parents('.one-task'));
			}
		},
		error: function(error){
			console.log(error);
		}
	});
}

function submitAddTask($th) {
	$.ajax({
			url: '/addTask',
			data: $th.closest('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
				getTasks()
			},
			error: function(error){
				console.log(error);
			}
		});
}

function submitAddSubTask($th) {
	$.ajax({
			url: '/addSubTask',
			data: $th.closest('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
				var taskId = $('#taskIdForSubtask').val();
				getTasks(taskId)
			},
			error: function(error){
				console.log(error);
			}
		});
}

function functionality(){

	$('#openAddForm').off('click');
	$('#openAddForm').click(function () {
		$('#addForm').addClass('showed');
		$('#addForm').find('[name=taskName]').focus()
	});

	$('.addNewSubTask').off('click');
	$('.addNewSubTask').click(function () {
		$('#addSubTaskForm').addClass('showed');
		var taskId = $(this).attr('data-taskId');
		$('#taskIdForSubtask').val(taskId)
		$('#curTaskName').val($(this).attr('data-taskname'));
		$('#addSubTaskForm').find('[name=subTaskName]').focus()
	});

	$('.btnCloseModal').click(function () {
		closeModals()
	});

	checkStatuses();

	$('.one-task').off('click');
	$('.one-task').click(function () {
		var $th = $(this);
		thisTask($th)
	});

	$('.one-subtask').off('mousedown')
	$('.one-subtask').mousedown(function (e) {
		if (e.which != 1){
			return
		}
		var tg = $(e.target);
		// console.log(tg.hasClass('removeSubTask'));
		// return
		var $th = $(this)
		if (tg.hasClass('one-subtask')){
			$th = tg
		} else {
			$th = tg.parents('.one-subtask')
		}

		if (tg.hasClass('removeSubTask') || tg.parents('.removeSubTask').length > 0){
			var taskId = $th.attr('data-subTaskId');
			var taskName = $th.attr('data-subtaskname');
			confirm_action('Confirm remove subtask ' + taskName,removeSubTask,taskId);
			console.log('remove');
		} else if (!$th.hasClass('completed')){
			completeSub($th.attr('data-subTaskId'));
			$th.addClass('completed');
			$th.find('input').attr('checked', 'checked');
			$th.find('input').prop('checked', 'checked');
			checkSubList($th);
			console.log('check');
		}
	});

	$('.removeTask').off('click');
	$('.removeTask').click(function () {
		var taskId = $(this).attr('data-taskId');
		var taskName = $(this).attr('data-taskname');
		confirm_action('Confirm removing task ' + taskName, removeTask, taskId)
	});
}

function confirm_action(text, w, taskId){
	Swal.fire({
        title: text,
        text: "Action requirement!",
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Remove now!',
        cancelButtonText: 'Back'
    }).then((result) => {
        if (result.value) {
            w(taskId);
        }
    });
}

$(function () {
	getTasks();


	$('#addForm').find('form').submit(function (e) {
		e.preventDefault()
		submitAddTask($('#btnAddTask'))
	});

	$('#addSubTaskForm').find('form').submit(function (e) {
		e.preventDefault();
		submitAddSubTask($('#btnAddSubTask'))
	})
});