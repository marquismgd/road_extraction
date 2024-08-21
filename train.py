from torch import nn,optim
from torch.utils.tensorboard import SummaryWriter

# default `log_dir` is "runs" - we'll be more specific here
writer = SummaryWriter('runs/fcn_sec')

from data import *
from net_fcn\
    import *
from torchvision.utils import save_image
from torch.utils.data import DataLoader
from utils import *

device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
weight_path=r'F:\unet\params_fcn_sec/'
data_path=r"F:\Columbus_paper\data"
save_path=r'F:\Columbus_paper\train_image_fcn_sec'

if __name__ == '__main__':
    # 创建Tensorboard对象

    data_loader=DataLoader(MyDataset(data_path),batch_size=1,shuffle=True)
    net=FCN().to(device)

    opt = optim.Adam(net.parameters())
    loss_fun=nn.BCELoss()


    epoch=1
    running_loss=0.0
    while epoch<=100:
        mkdir(f'{save_path}/{epoch}')


        for i,(image,label_image) in enumerate(data_loader):
            image,label_image=image.to(device),label_image.to(device)
            #label_image=torch.unsqueeze(label_image,0)
            out_image=net(image)
            train_loss=loss_fun(out_image,label_image)

            opt.zero_grad()
            train_loss.backward()
            opt.step()


            if i%20==0:
                print(f'{epoch}epoch-{i}th_image-train_loss======>>>{train_loss.item()}')

            #if i%50==0:
                #torch.save(net.state_dict(),f'{weight_path}{epoch}th_epoch.pth)

                _image = image[0][:3, :, :]
                _label_image = label_image.repeat(1,3,1,1)[0]*255
                _out_image = out_image.repeat(1,3,1,1)[0]*255

                img = torch.stack([_image,_label_image, _out_image], dim=0)
                save_image(img, f'{save_path}/{epoch}/{i}.tif')


            running_loss = train_loss.item()
            if i % 10 == 1:  # every 1000 mini-batches...

                # ...log the running loss
                writer.add_scalar('training loss',running_loss,i+epoch*len(data_loader))

        if epoch % 1 == 0:
            torch.save(net.state_dict(), f'{weight_path}{epoch}th_fcn.pth')
            print('save successfully!')
        epoch=epoch+1


