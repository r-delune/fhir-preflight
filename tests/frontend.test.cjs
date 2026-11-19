const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

function setup() {
  function element() {
    const classes = new Set();
    return {
      hidden: false, disabled: false, textContent: '', offsetTop: 100,
      attributes: {}, listeners: {}, dataset: {},
      classList: {add: c => classes.add(c), remove: c => classes.delete(c)},
      hasClass: c => classes.has(c),
      addEventListener(name, fn) {this.listeners[name] = fn;},
      setAttribute(name, value) {this.attributes[name] = value;},
      removeAttribute(name) {delete this.attributes[name];},
      scrollTo(options) {this.lastScroll = options;},
    };
  }
  const ids = Object.fromEntries([
    'json-view', 'selected-id', 'selected-message', 'location-note', 'selection-detail',
    'review-placeholder', 'validation-form', 'validate-button', 'validate-label',
    'busy-message', 'fixture'
  ].map(id => [id, element()]));
  for (let i = 1; i <= 10; i++) {
    ids[`line-${i}`] = element();
    ids[`line-${i}`].offsetTop = 100 + i * 20;
  }
  const cards = [element(), element()];
  cards[0].dataset = {start: '4', end: '5', issueId: 'VAL-TEST1',
    note: 'Matching JSON location highlighted.', message: '<b>untrusted text</b>'};
  cards[1].dataset = {start: '8', end: '8', issueId: 'VAL-TEST2',
    note: 'Closest matching parent highlighted.', message: 'Missing field'};
  const window = {listeners: {}, addEventListener(name, fn) {this.listeners[name] = fn;}};
  const document = {
    getElementById: id => ids[id],
    querySelectorAll: selector => selector === '.issue-card' ? cards :
      Object.values(ids).filter(e => e.hasClass('highlighted')),
  };
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../app/static/workbench.js'), 'utf8'),
    {document, window});
  return {ids, cards, window};
}

test('REQ-13: selecting a finding highlights its range, clears old selection and uses textContent', () => {
  const {ids, cards} = setup();
  cards[0].listeners.click();
  assert.equal(ids['line-4'].hasClass('highlighted'), true);
  assert.equal(ids['line-5'].hasClass('highlighted'), true);
  assert.equal(ids['selected-message'].textContent, '<b>untrusted text</b>');
  assert.equal(ids['json-view'].lastScroll.top, 40);
  assert.equal(cards[0].attributes['aria-pressed'], 'true');
  cards[1].listeners.click();
  assert.equal(ids['line-4'].hasClass('highlighted'), false);
  assert.equal(ids['line-8'].hasClass('highlighted'), true);
  assert.equal(cards[0].attributes['aria-pressed'], 'false');
  assert.equal(ids['location-note'].textContent, 'Closest matching parent highlighted.');
  assert.equal(ids['selection-detail'].hidden, false);
  assert.equal(ids['review-placeholder'].hidden, true);
});

test('REQ-14: fixture changes load the selected example and prevent validation of old data', () => {
  const {ids} = setup();
  let submitted = false;
  ids.fixture.listeners.change({target: {form: {requestSubmit() {submitted = true;}}}});
  assert.equal(submitted, true);
  assert.equal(ids['validate-button'].disabled, true);
  assert.equal(ids['validate-label'].textContent, 'Loading example…');
});

test('REQ-14: validation shows progress and back/forward restore permits another run', () => {
  const {ids, window} = setup();
  ids['validation-form'].listeners.submit();
  assert.equal(ids['validate-button'].disabled, true);
  assert.equal(ids['busy-message'].hidden, false);
  assert.equal(ids['validation-form'].attributes['aria-busy'], 'true');
  window.listeners.pageshow();
  assert.equal(ids['validate-button'].disabled, false);
  assert.equal(ids['busy-message'].hidden, true);
  assert.equal(ids['validation-form'].attributes['aria-busy'], undefined);
});
