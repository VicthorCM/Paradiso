import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ObrasPage } from './obras.page';

describe('ObrasPage', () => {
  let component: ObrasPage;
  let fixture: ComponentFixture<ObrasPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(ObrasPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
