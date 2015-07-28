jQuery(function($) {
  function updateNewInstitutionFieldStatus() {
    var $inst = $('#id_institutionId');
    if ($inst.val() === '-1') {
      $('#id_institutionName').parent().removeClass('hide').addClass('required');
      $('#id_institutionName').attr('required', 'required');
    } else {
      $('#id_institutionName').parent().addClass('hide').removeClass('required');
      $('#id_institutionName').attr('required', null);
    }
  }
  $('#id_institutionId').on('change', updateNewInstitutionFieldStatus);
  updateNewInstitutionFieldStatus();

  $('#id_institutionId').children().last().wrap('<optgroup label="Not Listed"></optgroup>');
  $('#id_departmentId').parent().after('<p><a tabindex="-1" href="#" id="id_institutionNotListed"><i class="fa fa-question-circle"></i> My Institution is not listed</a></p>')

  $('#id_institutionNotListed').on('click', function(e) {
    e.preventDefault();
    $('#id_institutionId').val(-1).trigger('change');
  });

});