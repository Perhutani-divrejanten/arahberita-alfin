/**
 * Example Google Apps Script function to trigger GitHub Actions repository_dispatch
 * Store your GitHub PAT in Script Properties as GITHUB_PAT and set REPO_OWNER and REPO_NAME
 */
function triggerGitHubDispatch(eventType) {
  const props = PropertiesService.getScriptProperties();
  const token = props.getProperty('GITHUB_PAT');
  const owner = props.getProperty('REPO_OWNER');
  const repo = props.getProperty('REPO_NAME');
  if (!token || !owner || !repo) throw new Error('Missing GITHUB_PAT / REPO_OWNER / REPO_NAME in Script Properties');

  const url = `https://api.github.com/repos/${owner}/${repo}/dispatches`;
  const payload = JSON.stringify({ event_type: eventType || 'sheet-edit' });
  const options = {
    method: 'post',
    contentType: 'application/json',
    headers: { Authorization: 'token ' + token, Accept: 'application/vnd.github.v3+json' },
    payload: payload,
    muteHttpExceptions: true
  };
  const resp = UrlFetchApp.fetch(url, options);
  Logger.log('dispatch response: ' + resp.getResponseCode() + ' ' + resp.getContentText());
  return resp.getResponseCode();
}

function onEditTrigger(e) {
  // call when you want to trigger deploy
  triggerGitHubDispatch('sheet-edit');
}
