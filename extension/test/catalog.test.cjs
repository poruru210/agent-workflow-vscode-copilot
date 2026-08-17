
const test = require('node:test');
const assert = require('node:assert/strict');
const { normalizeCatalog } = require('../out/catalog.js');

test('normalizes, filters, and sorts without inventing ranking metadata', () => {
  const input = [
    {name:'Zeta', id:'z', vendor:'v2', family:'f', version:'2', maxInputTokens:1000},
    {name:'Alpha', id:'a', vendor:'v1', family:'g', version:'1', maxInputTokens:500},
    {name:'Beta', id:'b', vendor:'v1', family:'g', version:'1', maxInputTokens:2000},
  ];
  const got = normalizeCatalog(input, {vendor:'v1', minInputTokens:600});
  assert.deepEqual(got, [{name:'Beta', id:'b', vendor:'v1', family:'g', version:'1', maxInputTokens:2000}]);
  const keys = Object.keys(got[0]).sort();
  assert.deepEqual(keys, ['family','id','maxInputTokens','name','vendor','version'].sort());
  assert.equal('costTier' in got[0], false);
  assert.equal('reasoning' in got[0], false);
  assert.equal('quality' in got[0], false);
});

test('uses null for absent public metadata and excludes missing capacity when a minimum is required', () => {
  const input = [{name:'A', id:'a'}, {name:'B', id:'b', maxInputTokens:900}];
  assert.equal(normalizeCatalog(input, {}).length, 2);
  assert.deepEqual(normalizeCatalog(input, {minInputTokens:800}), [
    {name:'B', id:'b', vendor:null, family:null, version:null, maxInputTokens:900}
  ]);
});
