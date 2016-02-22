$.getScript(base+"plugins/bootstrap-validator/bootstrapValidator.min.js", function(){
    $(document).ready(function() {
        var faIcon = {
            valid: 'fa fa-check-circle fa-lg text-success',
            invalid: 'fa fa-times-circle fa-lg',
            validating: 'fa fa-refresh'
        }

        $(form).bootstrapValidator({
            feedbackIcons: faIcon,
            excluded: ':disabled',
            fields: fields
        }).on('success.field.bv', function(e, data) {
            // $(e.target)  --> The field element
            // data.bv      --> The BootstrapValidator instance
            // data.field   --> The field name
            // data.element --> The field element

            var $parent = data.element.parents('.form-group');

            // Remove the has-success class
            $parent.removeClass('has-success');
        });
    });
});