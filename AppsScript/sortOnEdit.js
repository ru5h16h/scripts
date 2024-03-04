// Set the target header.
var targetColumnHeader = 'Priority'
// Set the target value.
var targetDefaultValue = -1
// Sort ascending or descending.
var sortAscending = true

/**
 * Checks if the given row is empty or not.
 *
 * @param {Object} sheet - The Google Sheet object.
 * @param {number} row - The row number to check.
 * @param {Array} ignoreIndices - Array of indices to ignore.
 * @return {boolean} Returns true if row is empty.
 */
function isRowEmpty(sheet, row, ignoreIndices) {
  var range = sheet.getRange(row, 1, 1, sheet.getLastColumn())
  var values = range.getValues()[0]
  for (var i = 0; i < values.length; i++) {
    if (values[i] !== '' && !ignoreIndices.includes(i)) {
      return false
    }
  }
  return true
}

/**
 * Sort sheet according to the given column index.
 */
function sortSheet(sheet, columnIndex) {
  var range = sheet.getRange('A2:Z')
  range.sort([{ column: columnIndex, ascending: sortAscending }])
}

function onEdit(event) {
  // Get the active sheet.
  var sheet = event.source.getActiveSheet()
  var editedRange = event.range

  // Sort the target column when the entry in it is updated.
  var editedColumn = editedRange.getColumn()
  var editedColumnHeader = sheet.getRange(1, editedColumn).getValue()
  var targetColumnIndex =
    sheet
      .getRange(1, 1, 1, sheet.getLastColumn())
      .getValues()[0]
      .indexOf(targetColumnHeader) + 1
  if (editedColumnHeader === targetColumnHeader) {
    sortSheet(sheet, targetColumnIndex)
  }

  // Add a default value to the target column whenever new row is added.
  var editedRow = editedRange.getRow()
  var targetCellValue = sheet.getRange(editedRow, targetColumnIndex).getValue()
  var isRowEmptyResult = isRowEmpty(sheet, editedRow, [targetColumnIndex])
  if (targetCellValue === '' && !isRowEmptyResult) {
    sheet.getRange(editedRow, targetColumnIndex).setValue(targetDefaultValue)
    sortSheet(sheet, targetColumnIndex)
  }
}
