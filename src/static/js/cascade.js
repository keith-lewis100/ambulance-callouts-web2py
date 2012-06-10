function cascadeSelect(parent, child){
    var childOptions = child.find('option:not(.static)');
    child.data('options',childOptions);

    parent.change(function(){
        childOptions.remove();
        child.append(child.data('options').filter('.sub_' + this.value))
            .change();
    })

    childOptions.not('.static, .sub_' + parent.val()).remove();
}

function createCascade(container, depth, baseid) {
    var parent = container.find('#' + baseid + 1);
    for (var level = 2; level <= depth; level++) {
        child = container.find('#' + baseid + level)
        cascadeSelect(parent, child);
        parent = child;
    }
}
