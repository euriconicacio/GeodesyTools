% UFPR - PPGCG - LARAS 
% 08/04/2018
% Script to compute normal heights by iterative method using orthometric
% heights and terrestrial gravity observations 

clear;
clc;
format long g;

% Input file full path - CHANGE!
input = 'C:\HN\Modelo_input.dat';

% Read data file
data  = load(input);

% GRS80 parameters - Hofmann-Wellenhof e Moritz (2005)
a = 6378137; % semimajor axis of the ellipsoid (m)
b = 6356752.3141; % semiminor axis of the ellipsoid (m)
f = 0.00335281068118; % flattening
nge = 9.7803267715; % normal gravity on the equator (m/s2)
ngp = 9.8321863685; % normal gravity on the pole (m/s2)
m = 0.00344978600308; % m = w^2*a^2 * (b/GM)

% Number rows (n) of the data matrix
n = length(data);

% Loop to compute normal heights (iterative method)
% Initialize zeros matrix --> will be used to store the iterations number
countm = zeros(n,1);

for i=1:n
% Normal gravity on the ellipsoid (Somigliana formula)
ng0(i,1) = (a * nge * (cosd(data(i,2)))^2 + b * ngp * (sind(data(i,2)))^2) / (a^2 * (cosd(data(i,2)))^2 + b^2 * (sind(data(i,2)))^2)^0.5;
% Input initial value for normal height (HN0)
HN0 = data(i,4);
% Set initial dif value
dif = 1e+10;
% Set initial count value
count = 0;

% simple Bouguer anomaly - calculated once for each point
deltagB = (data(i,5) + 0.1967*data(i,4)-ng0(i,1)*100000)/100000;

% Iterate while dif is not zero (by point)
 while(abs(dif) > 1e-12) 
     % Mean normal gravity compute
     gn = ng0(i,1) * (1 - (HN0/a) * (1 + f + m -(2*f) * (sind(data(i,2)))^2) + (HN0/a)^2);
     % Normal height compute
     HN = data(i,4)*(1-deltagB/gn);
     % Difference between the previous and the current height
     dif = HN0 - HN;
     HN0 = HN;
     % count the number of iterations by point
     count = count + 1; 
 end
 % Stores the the total number of iterations in the matrix "countm"
 countm(i,1) = count;
 % Stores in "min_dif" the minimum difference compute
 min_dif(i,1) = dif;
 % Stored in "iter" the number of iterations by point
 iter(i,1) = count;
 % Stored in "Hnor" the compute normal height by point
 Hnor(i,1) = HN;
 % Stored in "gnor" the compute mean normal gravity by point, in mGal
 gnor(i,1) = gn;
 % Stored in "C" the geopotential number, in kGal.m = m²/s²
 C(i,1) = HN*gn*0.1;
 
 i
end

% Store in "data_H" the input data and the obtained results 
data_H = [data Hnor C];

% Output file full path - CHANGE!
output = 'C:\HN\Modelo_output.dat';

file = fopen(output, 'w');
for ii = 1:size(data_H, 1)
    fprintf(file, '%d\t%f\t%f\t%.2f\t%.3f\t%.10f\t%.10f\n', data_H(ii, 1), data_H(ii, 2), data_H(ii, 3), data_H(ii, 4), data_H(ii, 5), data_H(ii, 6), data_H(ii, 7));
end
fclose(file);

disp('DONE!');
