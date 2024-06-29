$(document).ready(function() {})

$('.js-update-db').on('click', function() {
    var inputField = $('<input autocomplete="off" autofocus id="" name="" class="usr-profile-input" placeholder="Enter postal code" type="text" onkeyup="enableSave()" />')
    // var submit_btn = $('<button id="" class="btn btn-success" type="submit">Save</button>')
    var thisParent = $(this).parent();
    var thisId = $(this).attr('id');

    // submit_btn.prop('disabled', true);

    $('#home-pc-container').width('35%')

    switch(thisId) {
        case 'upd-homePc':
            inputField.attr({'id':'pc_residence', 'name': 'resid-postal-code'});
            // submit_btn.attr('id', 'upd-homePc');
            $('#home-pc-container').find('p').remove();

            if ($('#pc_residence').length < 1) {
                $('#home-pc-container').append(inputField);
            }

            break;

        case 'upd-workPc':
            inputField.attr({'id':'pc_work', 'name': 'work-postal-code'});
            // submit_btn.attr('id', 'upd-workPc');
            $('#work-pc-container').find('p').remove();

            if ($('#pc_work').length < 1) {
                $('#work-pc-container').append(inputField);
            }

            break;
    }

    $(this).remove();

});

function enableSave(btn) {
    if ($(event.target).val().length > 2) {
        $(event.target).parent().next('button').prop('disabled', false);
    }
}

$('#usr_profile_btn').on('click', function(e) {
    var commuteDaysInputs = $('#commuting-days-select').find('.input-group');
    var commuteDaysArr = [];
    var departTimeIntputs = $('#DepartTimeSelect').find('.input-group');
    var returnTimeIntputs = $('#returnTimeSelect').find('.input-group');
    var usr_departTime;
    var usr_returnTime;
    var user_home_pc = $('#pc_residence').val();
    var user_work_pc = $('#pc_work').val();

    $(commuteDaysInputs).each(function(i){
        var input = $(this).find('input');
        if (input[0].checked) {
            commuteDaysArr.push(input.val())
        }
    });

    $(departTimeIntputs).each(function(i){
        var input = $(this).find('input');
        if (input[0].checked) {
            usr_departTime = input.val()
        }
    });

    $(returnTimeIntputs).each(function(i){
        var input = $(this).find('input');
        if (input[0].checked) {
            usr_returnTime = input.val()
        }
    });

    $.ajax({
        url: '/',
        type: 'POST',
        data: {
            commute_days: commuteDaysArr,
            usr_departTime: usr_departTime,
            usr_returnTime: usr_returnTime,
            u_home_pc: user_home_pc,
            u_work_pc: user_work_pc
        },
        success: function() {
            console.log('Submit OK')
        },
        error: function(error) {
            console.log(error)
        }
    });

    e.preventDefault();
})

