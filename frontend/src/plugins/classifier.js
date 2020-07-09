export default function classify(objArr) {
  // classify object array to 'done' or 'undo'
  let returnObj = {
    done: [],
    undo: []
  };
  for (let i = 0; i < objArr.length; i++) {
    let data = objArr[i];
    if (data["status"] === 0) {
      returnObj.undo.push(data);
    } else if (data["status"] === 1) {
      returnObj.done.push(data);
    }
  }
  return returnObj;
}
