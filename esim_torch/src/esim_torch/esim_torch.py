import torch
import esim_cuda

# 下面这个类import的时候会name为ESIM
class EventSimulator_torch(torch.nn.Module):
    def __init__(self, contrast_threshold_neg=0.2, contrast_threshold_pos=0.2, refractory_period_ns=0):
        self.contrast_threshold_neg = contrast_threshold_neg
        self.contrast_threshold_pos = contrast_threshold_pos
        self.refractory_period_ns = int(refractory_period_ns)

        self.initial_reference_values = None
        self.timestamps_last_event = None
        self.last_image = None
        self.last_time = None

    def _check_inputs(self, images, timestamps):
        assert timestamps.dtype == torch.int64, timestamps.dtype
        assert images.dtype == torch.float32, images.dtype

    def reset(self):
        self.initial_reference_values = None
        self.last_image = None
        self.last_time = None

    # 这个函数的作用是将输入的图像和时间戳转换为events
    def forward(self,
                images, 
                timestamps):

        if len(images.shape) == 2:
            images = images.unsqueeze(0) #增加一个维度
        if len(timestamps.shape) == 0:
            timestamps = timestamps.unsqueeze(0)

        # 检查输入的images和timestamps的数据类型
        self._check_inputs(images, timestamps)

        if self.initial_reference_values is None:
            self.initial_reference_values = images[0].clone()
            self.timestamps_last_event = torch.zeros_like(self.initial_reference_values).long()

        if self.last_image is not None:
            images = torch.cat([self.last_image, images], 0)
            timestamps = torch.cat([self.last_time, timestamps], 0)

        if len(images) == 1:
            self.last_image = images[-1:]
            self.last_time = timestamps[-1:]
            return None
        
        # 这个才是初始化去处理的
        events = self.initialized_forward(images, timestamps)

        self.last_image = images[-1:]
        self.last_time = timestamps[-1:]
        # 把结果返回
        return events

    def initialized_forward(self, images, timestamps):

        T, H, W = images.shape
        reference_values_over_time = torch.zeros((T-1, H, W),
                                                 device=images.device,
                                                 dtype=images.dtype)

        event_counts = torch.zeros_like(images[0]).long()

        # 运行的是esim_forward_count_events
        reference_values_over_time, event_counts = esim_cuda.forward_count_events(images, 
                                                                                  self.initial_reference_values,
                                                                                  reference_values_over_time,
                                                                                  event_counts,
                                                                                  self.contrast_threshold_neg,
                                                                                  self.contrast_threshold_pos)

        # compute the offsets for each event group
        cumsum = event_counts.view(-1).cumsum(dim=0)
        total_num_events = cumsum[-1]
        offsets = cumsum.view(H, W) - event_counts

        # compute events on the GPU
        events = torch.zeros((total_num_events, 4), device=cumsum.device, dtype=cumsum.dtype)

        # 注意此处就是调用cu文件的esim_forward
        events = esim_cuda.forward(images,
                                   timestamps,
                                   self.initial_reference_values,
                                   reference_values_over_time,
                                   offsets,
                                   events,
                                   self.timestamps_last_event,
                                   self.contrast_threshold_neg,
                                   self.contrast_threshold_pos,
                                   self.refractory_period_ns)


        # sort by timestamps. Do this for each batch of events
        if len(events) == 0:
            return None
        # 按照时间戳排序
        events = events[events[:,2].argsort()]
        events = events[events[:,2]>0]

        self.initial_reference_values = reference_values_over_time[-1]
        # 返回一个字典，包含x,y,t,p
        return dict(zip(['x','y','t','p'], events.T))