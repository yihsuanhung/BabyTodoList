export default function process(objArr) {
  // add edit status and edit content to fetched data
  let processed = [];
  for (let i = 0; i < objArr.length; i++) {
    let obj = objArr[i];
    obj["editStatus"] = false;
    obj["editContent"] = "";
    processed.push(obj);
  }
  return processed;
}
