<template>
  <div>
    <button @click="taskdone()">Done</button>
  </div>
</template>

<script>
import sendReq from "@/plugins/sendReq";
import { API } from "@/constants/config";
import { EventBus } from "@/plugins/bus.js";
export default {
  name: "Done",
  props: ["inPage", "inLimit"],
  data() {
    return {
      apiURL: API.Host + ":" + API.Port,
      selection: []
    };
  },
  methods: {
    async taskdone() {
      if (this.selection.length !== 0) {
        for (let i = 0; i < this.selection.length; i++) {
          let taskId = this.selection[i];
          let config = {
            baseURL: this.apiURL,
            url: "/done/" + Number(taskId),
            method: "put",
            params: {
              page: this.inPage,
              limit: this.inLimit
            }
          };
          let result = await sendReq(config);
          console.log(result);
          let data = result["data"];
          this.$emit("outData", data);
          this.outData = data;
        }
        EventBus.$emit("TasksSelectionBus", []);
        this.$forceUpdate();
      }
    }
  },
  created() {
    EventBus.$on("TasksSelectionBus", arr => {
      this.selection = arr;
    });
  },
  beforeDestroy: function() {
    EventBus.$off();
  }
};
</script>
