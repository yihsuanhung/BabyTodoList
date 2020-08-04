<template>
  <div>
    <button @click="taskundo()">Undo</button>
  </div>
</template>

<script>
import sendReq from "@/plugins/sendReq";
import { API } from "@/constants/config";
import { EventBus } from "@/plugins/bus.js";
export default {
  name: "Undo",
  props: ["inPage", "inLimit"],
  data() {
    return {
      apiURL: API.Host + ":" + API.Port,
      selection: []
    };
  },
  methods: {
    async taskundo() {
      if (this.selection.length !== 0) {
        for (let i = 0; i < this.selection.length; i++) {
          let taskId = this.selection[i];
          let config = {
            baseURL: this.apiURL,
            url: "/undo/" + Number(taskId),
            method: "put",
            params: {
              page: this.inPage,
              limit: this.inLimit
            }
          };
          let result = await sendReq(config);
          let data = result["data"];
          this.$emit("outData", data);
        }
        this.$forceUpdate();
      }
      EventBus.$emit("TasksSelectionBus", []);
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
