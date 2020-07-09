<template>
  <div>
    <table align="center">
      <td v-for="(item, index) in this.maxPage" :key="index">
        <button @click="pageindex(item)">{{ item }}</button>
      </td>
    </table>
  </div>
</template>

<script>
import sendReq from "@/plugins/sendReq";
import { API } from "@/constants/config";
export default {
  name: "Pagination",
  props: ["page", "limit", "dbLen", "maxPage"],
  data() {
    return {
      apiURL: API.Host + ":" + API.Port,
      outData: [],
      pageconfig: {
        page: this.page,
        limit: this.limit,
        dbLen: this.dbLen
        // maxPage: this.maxPage
      }
    };
  },
  methods: {
    async pageindex(pag) {
      let config = {
        baseURL: this.apiURL,
        url: "/index",
        method: "get",
        params: {
          page: pag,
          limit: this.pageconfig.limit
        }
      };
      this.pageconfig.page = pag;
      let result = await sendReq(config);
      let data = result["data"];
      this.$emit("TaskOutIndex", data);
      this.$emit("PagesOut", {
        page: this.pageconfig.page,
        limit: this.pageconfig.limit
      });
    }
  }
};
</script>
