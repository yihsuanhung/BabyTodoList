import axios from "axios";

export default async function SendReq(config) {
  let result = { status: 9, msg: "function err" };
  await axios.request(config).then(resp => {
    result = resp.data;
  });
  //   .catch(
  //     (err) =>{
  //       var result = {'status':10}
  //     }
  //   )
  return result;
}
