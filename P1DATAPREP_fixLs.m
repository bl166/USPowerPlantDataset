% Fix landsat image issue
fprintf('Fixing landsat imagery: normalizing...\n')

% get paths, default file format being geotiff
path = pwd;
path = fullfile(path,'uspp_landsat');
ext = '*.tif';

files = [];
files = [files, dir(fullfile(path,ext))];

% conversion from single to normalized double
fprintf('|     Progress     |\n')
progressIntervals = ceil(length(files)/20);
for i=1:length(files)
    map=(imread(fullfile(path,files(i).name)));
	im=imadjust(map,[0.03; 0.3],[0; 1],1.4) ;
    imwrite(mat2gray(im),fullfile(path,files(i).name))
    if i~=1 && ~mod(i-1,progressIntervals)
    	fprintf('|')
    end
end
fprintf('|\n')
msg = [num2str(length(files)),' images done!\n'];
fprintf(msg)

quit