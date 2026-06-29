const vscode = require('vscode');

/**
 * Called when the extension is activated (first .yo file opened).
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('YO Language extension activated.');

    // ── "Run YO File" command ──
    const runCommand = vscode.commands.registerCommand('yo.runFile', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active file to run.');
            return;
        }

        const filePath = editor.document.fileName;
        if (!filePath.endsWith('.yo')) {
            vscode.window.showWarningMessage('Current file is not a .yo file.');
            return;
        }

        // Save the file before running
        editor.document.save().then(() => {
            // Reuse or create a dedicated terminal
            let terminal = vscode.window.terminals.find(t => t.name === 'YO Runner');
            if (!terminal) {
                terminal = vscode.window.createTerminal('YO Runner');
            }
            terminal.show();
            terminal.sendText(`yo run "${filePath}"`);
        });
    });

    context.subscriptions.push(runCommand);
}

/**
 * Called when the extension is deactivated.
 */
function deactivate() {}

module.exports = {
    activate,
    deactivate
};
