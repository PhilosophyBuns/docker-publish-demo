<template>
  <task-work-area width="500" height="500" :ini="ini_config" :id="work_id" v-on:on-add-nodemodel="onAddNodeModel" v-on:on-mouse="onMouse">
    <!-- 这里就是包含节点、路径 等-->
  </task-work-area>
</template>
<script>
export default {
  data () {
    return {
      work_id: 'work_id',
      ini_config: {
        lineType: 'Q',
        isDotted: false,
        scaling: {
          ZoomX: 1,
          ZoomY: 1
        }
      }
    }
  },
  methods: {
    onMouse: function (event, workId) {
      console.log('鼠标右击工作区事件！', event, workId)
    },
    onAddNodeModel (event, node) {
      console.log('添加节点', event.clientX, event.clientY, node)
      let newNode = {}
      newNode = node
      newNode.id = 'node' + Math.floor(Math.random() * 100)
      newNode.positionX = node.positionX - 90 // -15 -90 定位到节点的终点
      newNode.positionY = node.positionY - 15
      newNode.outPorts = [{
        id: newNode.id + '_' + Math.floor(Math.random() * 10)
      }]
      newNode.inPorts = []
      this.nodes.push(newNode)
    }
  }
}
</script>
