/**
 * Created by zmbq on 6/4/14.
 */

function customHtmlFormatter(cellValue, options, rowObject) {
    var col = options.colModel.name
    var html = rowObject.html[col]

    return html || rowObject[col]
}

function getGridRowElement(grid, rowId) {
    return $("tr[id=" + rowId +"]", grid);
}

function getGridCellElement(grid, rowId, colName) {
    // Returns the td element of a cell. This is done by looking at the aria-describedby attribute, which
    // is grid_colname (grid probably being the name of the grid)
    var row = getGridRowElement(grid, rowId);
    var col = $('td[aria-describedby$=_' + colName + ']', row);
    return col;
}

function disableRowInputs(grid, rowId) {
    // Disable all the inputs of a row.
    // Disabling a checkbox requires using jQuery (and not grid.setCell), so we use jQuery for the whole thing

    var row = getGridRowElement(grid, rowId);

    var checkbox = $("input[type='checkbox']", row)
    checkbox.attr('disabled', true) // Disable the checkbox

    var tds = $("td", row)
    tds.addClass("not-editable-cell")

    // TODO: Disable dropdowns
}
